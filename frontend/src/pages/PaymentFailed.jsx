import { useNavigate } from "react-router-dom";

function PaymentFailed() {

  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>

      <h1>Payment Failed</h1>

      <p>Your payment could not be completed.</p>

      <button
        onClick={() => navigate("/cart")}
        style={{
          padding: "10px 20px",
          background: "#dc3545",
          color: "white",
          border: "none",
          cursor: "pointer"
        }}
      >
        Try Again
      </button>

    </div>
  );
}

export default PaymentFailed;