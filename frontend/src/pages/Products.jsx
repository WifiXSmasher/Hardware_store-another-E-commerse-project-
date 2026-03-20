import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function Products() {

  const [products, setProducts] = useState([]);

  useEffect(() => {

    api.get("products/")
      .then((response) => {
        setProducts(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  }, []);

  return (
    <div style={{ padding: "20px" }}>

      <h1>Products</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(250px,1fr))",
        gap: "20px"
      }}>

        {products.map(product => {

          const image =
            product.images.length > 0
              ? product.images[0].image
              : null;

          return (
            <div
              key={product.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "15px"
              }}
            >

              {image && (
                <img
                  src={image}
                  alt={product.name}
                  style={{
                    width: "100%",
                    height: "180px",
                    objectFit: "cover"
                  }}
                />
              )}

              <h3>{product.name}</h3>

              <p><b>Brand:</b> {product.brand}</p>

              <p><b>Price:</b> ₹{product.price}</p>
              {/* <p><b>Stock:</b> {product.stock}</p> */}

              <Link to={`/product/${product.id}`}>
                <button>View Details</button>
              </Link>

            </div>
          );

        })}

      </div>

    </div>
  );
}

export default Products;