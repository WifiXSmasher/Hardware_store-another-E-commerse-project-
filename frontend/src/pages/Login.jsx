import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";

function Login() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const { login } = useContext(AuthContext);

  const handleLogin = () => {

    api.post("auth/login/", {
      username,
      password
    })
    .then((response) => {

      login(response.data.access, response.data.refresh);

      alert("Login successful");

      navigate("/");

    })
    .catch((error) => {
      console.error(error);
      alert("Login failed");
    });

  };

  return (
    <div>

      <h1>Login</h1>

      <input
        placeholder="Username"
        onChange={(e)=>setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>
        Login
      </button>
        <Link to="/forgot-password">
            Forgot Password?
        </Link>
    </div>
  );
}

export default Login;