import React from "react";
import { AiFillCopyrightCircle } from "react-icons/fa";

export default function Footer({style="fixed"}) {
  return (
    <div className="footer" style={{"position": style}}>
      © Carleton College Aequitas
    </div>
  );
}
