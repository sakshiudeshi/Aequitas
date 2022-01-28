import React, { useEffect, useState } from "react";

export default function DragAndDrop({ handleDrop, children }) {
  const [dragging, setDragging] = useState(false);
  var dragCounter = 0;

  const overrideEventDefaults = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const createDragAndDropOverlay = (e) => {
    overrideEventDefaults(e);
    dragCounter++;
    setDragging(true);
  };

  const removeDragAndDropOverlay = (e) => {
    overrideEventDefaults(e);
    dragCounter--;
    if (dragCounter < 0) setDragging(false);
  };

  //https://www.c-sharpcorner.com/article/file-drag-and-drop-feature-in-reactjs/
  const handleDragAndDropFiles = (e) => {
    overrideEventDefaults(e);
    dragCounter = 0;
    setDragging(false);
    if (!e.dataTransfer) return;
    handleDrop(e.dataTransfer.files[0]);
    e.dataTransfer.clearData();
  };

  return (
    <div>
      {
        <div
          id="dragAndDropContainer"
          className="dragAndDropContainer"
          onDrop={overrideEventDefaults}
          onDragEnter={overrideEventDefaults}
          onDragLeave={overrideEventDefaults}
          onDragOver={overrideEventDefaults}
        >
          <div
            id="dragAndDropArea"
            className="dragAndDropArea"
            onDrop={handleDragAndDropFiles}
            onDragEnter={createDragAndDropOverlay}
            onDragLeave={removeDragAndDropOverlay}
            onDragOver={overrideEventDefaults}
          >
            {children}
            {dragging && (
              <div
                style={{
                  border: "dashed grey 4px",
                  backgroundColor: "rgba(255,255,255,.8)",
                  position: "absolute",
                  top: 0,
                  bottom: 0,
                  left: 0,
                  right: 0,
                  zIndex: 9999,
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    top: "50%",
                    right: 0,
                    left: 0,
                    textAlign: "center",
                    color: "grey",
                    fontSize: 36,
                  }}
                >
                  <div>drop here :)</div>
                </div>
              </div>
            )}
          </div>
        </div>
      }
    </div>
  );
}
