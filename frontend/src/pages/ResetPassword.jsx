import { useParams } from "react-router-dom";
import { useState } from "react";
import api from "../services/api";

function ResetPassword() {

  const { uid, token } = useParams();

  const [password, setPassword] = useState("");

  const resetPassword = () => {

    api.post("auth/password-reset-confirm/", {
      uid: uid,
      token: token,
      password: password
    })
    .then(() => {
      alert("Password reset successful");
    })
    .catch((err) => {
      console.log(err.response.data);
      alert("Reset failed");
    });

  };

  return (
    <div>

      <h1>Reset Password</h1>

      <input
        type="password"
        placeholder="New password"
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={resetPassword}>
        Reset Password
      </button>

    </div>
  );
}

export default ResetPassword;