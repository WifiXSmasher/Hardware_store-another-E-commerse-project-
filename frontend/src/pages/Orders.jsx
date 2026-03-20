import { useEffect, useState } from "react";
import api from "../services/api";

function Orders() {

  const [orders, setOrders] = useState([]);

  useEffect(() => {

    api.get("orders/")
      .then((response) => {
        setOrders(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  }, []);

  return (
    <div style={{ padding: "20px" }}>

      <h1>Your Orders</h1>

      {orders.length === 0 && <p>No orders found.</p>}

      {orders.map(order => (

        <div
          key={order.id}
          style={{
            border: "1px solid #ccc",
            padding: "15px",
            marginBottom: "20px"
          }}
        >

          <h3>Order #{order.id}</h3>

          <p><b>Total:</b> ₹{order.total_amount}</p>

          <p><b>Date:</b> {new Date(order.created_at).toLocaleString()}</p>

          <h4>Items</h4>

          {order.items.length === 0 ? (
            <p>No items</p>
          ) : (
            order.items.map((item, index) => (

              <div key={index} style={{ marginBottom: "5px" }}>

                {item.name} — ₹{item.price} × {item.quantity}

              </div>

            ))
          )}

        </div>

      ))}

    </div>
  );
}

export default Orders;