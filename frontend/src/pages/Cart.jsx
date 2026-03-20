import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Cart() {

  const [items, setItems] = useState([]);

  const navigate = useNavigate();

  const fetchCart = () => {

    api.get("cart/")
      .then((response) => {

        setItems(response.data);

      })
      .catch((error) => {

        console.error("Failed to load cart", error);

      });

  };

  useEffect(() => {

    fetchCart();

  }, []);

  const removeItem = (id) => {

    api.delete(`cart/remove/${id}/`)
      .then(() => {

        fetchCart();

      })
      .catch((error) => {

        console.error("Failed to remove item", error);

      });

  };

  const checkout = async () => {

    try {

      const orderResponse = await api.post("payments/create-order/");

      const order = orderResponse.data;

      const options = {

        key: "rzp_test_STHkDtYLsktMRs", // replace with your Razorpay test key

        amount: order.amount,

        currency: "INR",

        name: "Hardware Shop",

        description: "Order Payment",

        order_id: order.razorpay_order_id,

        handler: async function (response) {

            try {

                await api.post("orders/checkout/", {
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_signature: response.razorpay_signature
                });

                navigate("/payment-success");

            } catch (error) {

                console.error(error);

                navigate("/payment-failed");

            }

        },

        theme: {
          color: "#28a745"
        }

      };

      const razorpay = new window.Razorpay(options);

      razorpay.open();

    } catch (error) {

      console.error("Payment initialization failed", error);

      alert("Payment failed to start");

    }

  };

  const total = items.reduce((sum, item) => {

    return sum + item.price * item.quantity;

  }, 0);

  return (

    <div style={{ padding: "20px" }}>

      <h1>Cart</h1>

      {items.length === 0 ? (

        <p>Your cart is empty</p>

      ) : (

        <>

          {items.map((item) => (

            <div
              key={item.id}
              style={{
                border: "1px solid #ccc",
                padding: "15px",
                marginBottom: "15px",
                borderRadius: "6px"
              }}
            >

              <h3>{item.name}</h3>

              <p>Price: ₹{item.price}</p>

              <p>Quantity: {item.quantity}</p>

              <p>
                Subtotal: ₹{item.price * item.quantity}
              </p>

              <button
                onClick={() => removeItem(item.id)}
                style={{
                  background: "#d9534f",
                  color: "white",
                  border: "none",
                  padding: "8px 12px",
                  cursor: "pointer"
                }}
              >
                Remove
              </button>

            </div>

          ))}

          <h2>Total: ₹{total}</h2>

          <button
            onClick={checkout}
            style={{
              background: "#28a745",
              color: "white",
              border: "none",
              padding: "10px 16px",
              fontSize: "16px",
              cursor: "pointer"
            }}
          >
            Pay with Razorpay
          </button>

        </>

      )}

    </div>

  );

}

export default Cart;