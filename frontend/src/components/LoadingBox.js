import React from "react";

export default function LoadingBox() {
  return (
    <div class="d-flex justify-content-center">
      <div className="spinner-border text-primary" style={{marginTop: '1rem', width: '3rem', height: '3rem'}} role="status">
      </div>
      <br/>
      loading...
    </div>
  );
}
