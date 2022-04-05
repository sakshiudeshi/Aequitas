import React from "react";

export default function Header({children}) {
  return (
    <div className="jumbotron">
      <h1 className="display-4">{children}</h1>
    </div>
  );
}