import { useState } from "react";
import api from "../services/api";

function ForgotPassword() {

  const [email, setEmail] = useState("");

  const submit = () => {

    api.post("auth/password-reset/", { email })
      .then(() => {
        alert("Reset email sent");
      })
      .catch((err) => {
        console.error(err);
      });

  };

  return (

    <div>

      <h1>Forgot Password</h1>

      <input
        placeholder="Enter your email"
        onChange={(e)=>setEmail(e.target.value)}
      />

      <button onClick={submit}>
        Send Reset Link
      </button>

    </div>

  );

}

export default ForgotPassword;