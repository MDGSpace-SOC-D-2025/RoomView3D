async function signup() {
  console.log("Signup button clicked");

  try {
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    alert(`${firstName} welcome to RoomView3D`);

    const res = await fetch("http://127.0.0.1:5000/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
      })
    });

    console.log("Response status:", res.status);

    const data = await res.json();
    console.log("Response data:", data);

    if (res.ok) {
      alert("Signup success");
    } else {
      alert(data.error);
    }

  } catch (err) {
    console.error("Signup error:", err);
    alert("Signup failed, check console");
  }
}


async function login() {
  console.log("Login button clicked");

  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log({ email, password });

    const res = await fetch("http://127.0.0.1:5000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const data = await res.json();
    console.log("Response status:", res.status);
    console.log("Response data:", data);

    if (!res.ok) {
      alert(data.error || "Login failed");
      return;
    }

    localStorage.setItem("token", data.token);

    alert("Login successful");


  } catch (err) {
    console.error("Login error:", err);
    alert("Login failed, check console");
  }
}

function googleLogin() {
  window.location.href = "http://127.0.0.1:5000/auth/google/login";
}


