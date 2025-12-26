from flask import Blueprint, request, jsonify, redirect
from auth.utils import (
    hash_password, 
    verify_password, 
    create_access_token, 
    validate_password_strength,
    validate_email_format,
    verify_token
)
from auth.google_oauth import (
    get_google_auth_url,
    exchange_code_for_token,
    get_google_user_info,
    verify_google_id_token
)
from models.users import (
    create_user_with_password,
    create_user_with_google,
    get_user_by_email,
    get_user_by_google_id,
    get_user_by_id,
    link_google_account
)
from functools import wraps

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Middlewares

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Authorization: Bearer xyz123
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify token
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Pass user_id to the route
        return f(payload['user_id'], *args, **kwargs)
    
    return decorated


# TRADITIONAL AUTH ROUTES 

@auth_bp.route('/signup', methods=['POST'])
def signup():

    try:
        data = request.get_json()
        
        # Extract data
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        
        # Validate required fields
        if not email or not password or not first_name or not last_name:
            return jsonify({
                'error': 'All fields are required'
            }), 400
        
        # Validate email format
        if not validate_email_format(email):
            return jsonify({
                'error': 'Invalid email format'
            }), 400
        
        # Validate password strength
        is_valid, message = validate_password_strength(password)
        if not is_valid:
            return jsonify({
                'error': message
            }), 400
        
        # Check if email already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({
                'error': 'Email already registered'
            }), 409
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user in database
        user, error = create_user_with_password(
            email, 
            password_hash, 
            first_name, 
            last_name
        )
        
        if error:
            return jsonify({
                'error': error,
            }), 500
        
        # Generate JWT token
        token = create_access_token(user['id'], user['email'])
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'firstName': user['first_name'],
                'lastName': user['last_name'],
                'authProvider': user['auth_provider']
            }
        }), 201
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
 
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({
                'error': 'Email and password are required'
            }), 400
        
        # Get user from database
        user = get_user_by_email(email)
        
        if not user:
            return jsonify({
                'error': 'Invalid email or password'
            }), 401
        
        # Check if user registered with Google
        if user['auth_provider'] == 'google' and not user.get('password_hash'):
            return jsonify({
                'error': 'This account uses Google Sign-In. Please use "Sign in with Google" button.'
            }), 403
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({
                'error': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token = create_access_token(user['id'], user['email'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'firstName': user.get('first_name'),
                'lastName': user.get('last_name'),
                'profilePicture': user.get('profile_picture'),
                'authProvider': user['auth_provider']
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500


# GOOGLE OAUTH ROUTES 

@auth_bp.route('/google/login')
def google_login():

    auth_url = get_google_auth_url()
    return redirect(auth_url)


@auth_bp.route('/google/callback')
def google_callback():

    try:
        # Get authorization code from query parameters
        code = request.args.get('code')
        
        if not code:
            return jsonify({
                'error': 'Authorization code not provided'
            }), 400
        
        # Exchange code for tokens
        token_data = exchange_code_for_token(code)
        
        if 'error' in token_data:
            return jsonify({
                'error': 'Failed to get access token',
                'details': token_data.get('error_description')
            }), 400
        
        access_token = token_data.get('access_token')
        id_token_str = token_data.get('id_token')
        
        # Verify ID token (security check)
        id_info = verify_google_id_token(id_token_str)
        
        if not id_info:
            return jsonify({
                'error': 'Invalid ID token'
            }), 401
        
        # Get user info from Google
        user_info = get_google_user_info(access_token)
        
        google_id = id_info['sub']  # Google user ID
        email = user_info['email']
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        picture = user_info.get('picture', '')
        
        # Check if user exists by Google ID
        user = get_user_by_google_id(google_id)
        
        if user:
            # User exists, log them in
            token = create_access_token(user['id'], user['email'])
            # Frontend will extract token from URL and store it
            frontend_url = f'http://127.0.0.1:5500/Frontend/index.html?token={token}'
            return redirect(frontend_url)
        
        # Check if user exists by email (signed up with email/password)
        user = get_user_by_email(email)
        
        if user:
            # Link Google account to existing user
            user = link_google_account(email, google_id, picture)
            
            if not user:
                return jsonify({
                    'error': 'Failed to link Google account'
                }), 500
            
            token = create_access_token(user['id'], user['email'])
            frontend_url = f'http://127.0.0.1:5500/Frontend/index.html?token={token}'
            return redirect(frontend_url)
        
        # User doesn't exist, create new account
        user, error = create_user_with_google(
            email,
            google_id,
            first_name,
            last_name,
            picture
        )
        
        if error:
            return jsonify({
                'error': 'Failed to create user',
                'details': error
            }), 500
        
        # Generate token and redirect
        token = create_access_token(user['id'], user['email'])
        frontend_url = f'http://127.0.0.1:5500/Frontend/index.html?token={token}'
        return redirect(frontend_url)
        
    except Exception as e:
        print(f"Google callback error: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500


# PROTECTED ROUTES (Examples) 

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id):

    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'user': {
                'id': user['id'],
                'email': user['email'],
                'firstName': user.get('first_name'),
                'lastName': user.get('last_name'),
                'profilePicture': user.get('profile_picture'),
                'authProvider': user['auth_provider'],
                'createdAt': user['created_at']
            }
        }), 200
        
    except Exception as e:
        print(f"Get user error: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500


@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token_route(user_id):

    return jsonify({
        'valid': True,
        'userId': user_id
    }), 200

