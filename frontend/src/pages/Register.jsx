import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const register = () => {

    api.post("auth/register/", {
      username,
      email,
      password
    })
    .then(() => {

      alert("Registration successful");

      navigate("/login");

    })
    .catch((error) => {

      console.error(error);

      alert("Registration failed");

    });

  };

  return (

    <div style={{ padding: "20px" }}>

      <h1>Register</h1>

      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={register}>
        Register
      </button>

    </div>

  );
}

export default Register;