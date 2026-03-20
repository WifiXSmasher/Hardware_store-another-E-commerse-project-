import { Link, useNavigate } from "react-router-dom";

//import context 
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";



function Navbar() {

  const navigate = useNavigate();
    
  const logout = () => {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    navigate("/login");

  };

  const token = localStorage.getItem("access_token");

  return (

    <div style={{
      background:"#222",
      padding:"15px",
      display:"flex",
      gap:"20px"
    }}>

      <Link to="/" style={{color:"white"}}>Products</Link>

      <Link to="/cart" style={{color:"white"}}>Cart</Link>

      <Link to="/orders" style={{color:"white"}}>Orders</Link>
      
      {token ? (
        <button onClick={logout}>
          Logout
        </button>
      ) : (
        <>
          <Link to="/login" style={{color:"white"}}>Login</Link>
          <Link to="/register" style={{color:"white"}}>Register</Link>
        </>
      )}

    </div>

  );
}

export default Navbar;