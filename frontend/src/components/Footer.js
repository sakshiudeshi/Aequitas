import React from "react";
import { AiFillCopyrightCircle } from "react-icons/fa";

export default function Footer({style="relative"}) {
  return (
    <div className="footer" style={{"position": style}}>
      © Carleton College Aequitas
    </div>
  );
}
