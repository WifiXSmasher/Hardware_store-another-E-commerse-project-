import { useNavigate } from "react-router-dom";

function PaymentSuccess() {

  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>

      <h1>Payment Successful</h1>

      <p>Your order has been placed successfully.</p>

      <button
        onClick={() => navigate("/orders")}
        style={{
          padding: "10px 20px",
          background: "#28a745",
          color: "white",
          border: "none",
          cursor: "pointer"
        }}
      >
        View Orders
      </button>

    </div>
  );
}

export default PaymentSuccess;