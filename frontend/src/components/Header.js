import React from "react";

export default function Header({child}) {
  return (
    <div className="jumbotron">
      {child}
    </div>
  );
}