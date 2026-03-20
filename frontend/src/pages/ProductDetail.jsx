import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

function ProductDetail() {

  const { id } = useParams();

  const [product, setProduct] = useState(null);

  const [productQuantity, setProductQuantity] = useState(1);

  const [partQuantities, setPartQuantities] = useState({});

  useEffect(() => {

    api.get(`products/${id}/`)
      .then((response) => {
        setProduct(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

  }, [id]);

  if (!product) {
    return <p>Loading...</p>;
  }

  // ---------- Add Spare Part ----------
  const addToCart = (sparePartId, quantity) => {
    if(quantity < 1 ){
        alert("Quantity must be more than 1 (nahi kyun karna hai ye sab)");
        return ;
    }
    api.post("cart/add/", {
      spare_part_id: sparePartId,
      quantity: quantity,
    })
    .then(() => {
      alert("Spare part added to cart");
    })
    .catch((error) => {
      console.error(error);
      alert("Failed to add spare part");
    });

  };

  // ---------- Add Product ----------
  const addProductToCart = () => {
    if(productQuantity < 1 ){
        alert("Quantity must be more than 1 (nahi kyun karna hai ye sab)");
        return ;
    }
    api.post("cart/add/", {
      product_id: product.id,
      quantity: productQuantity
    })
    .then(() => {
      alert("Product added to cart");
    })
    .catch((error) => {
      console.error(error);
      alert("Failed to add product");
    });

  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>{product.name}</h1>

      <p><b>Brand:</b> {product.brand}</p>

      <p><b>Description:</b> {product.description}</p>

      <p><b>Stock:</b> {product.stock}</p>

      <p><b>Price:</b> ₹{product.price}</p>

      {/* Product Quantity Selector */}

      <div style={{ marginBottom: "10px" }}>
        <input
          type="number"
          min="1"
          max={product.stock}
          value={productQuantity}
          onChange={(e) => setProductQuantity(Number(e.target.value))}
          style={{ width: "60px", marginRight: "10px" }}
        />

        <button
          disabled={product.stock === 0}
          onClick={addProductToCart}
        >
          {product.stock === 0 ? "Out of Stock" : "Add Product To Cart"}
        </button>
      </div>

      {/* Images */}

      <h2>Images</h2>

      <div style={{ display: "flex", gap: "10px" }}>
        {product.images.map(img => (
          <img
            key={img.id}
            src={img.image}
            alt="product"
            style={{ width: "200px" }}
          />
        ))}
      </div>

      {/* Spare Parts */}

      <h2>Spare Parts</h2>

      {product.spare_parts.map(part => (

        <div
          key={part.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginTop: "10px"
          }}
        >

          <h4>{part.name}</h4>

          <p>Price: ₹{part.price}</p>

          <p>Stock: {part.stock}</p>

          <img
            src={part.image}
            alt={part.name}
            style={{ width: "150px" }}
          />

          <br /><br />

          {/* Spare Part Quantity */}

          <input
            type="number"
            min="1"
            max={part.stock}
            value={partQuantities[part.id] || 1}
            onChange={(e) =>
              setPartQuantities({
                ...partQuantities,
                [part.id]: Number(e.target.value)
              })
            }
            style={{ width: "60px", marginRight: "10px" }}
          />

          <button
            disabled={part.stock === 0}
            onClick={() => addToCart(part.id, partQuantities[part.id] || 1)}
          >
            {part.stock === 0 ? "Out of Stock" : "Add to Cart"}
          </button>

        </div>

      ))}

    </div>
  );
}

export default ProductDetail;