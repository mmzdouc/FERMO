document.addEventListener('DOMContentLoaded', function() {
    var dragged;

    document.addEventListener("drag", function(event) {
    }, false);

    document.addEventListener("dragstart", function(event) {
        dragged = event.target;
        // make it half transparent
        event.target.style.opacity = .5;
        event.dataTransfer.setData("draggedAccId", event.target.id);
        setTimeout(() => event.target.classList.toggle("hidden"));
        // change dropzone background when hovering
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "#a3a3a3";
        }
        // highlight dropzones
        document.querySelectorAll('.dropzone').forEach(function(dropzone) {
            dropzone.classList.add('dropzone-dragging');
        });
    }, false);

    document.addEventListener("dragend", function(event) {
        // reset the transparency
        event.target.style.opacity = "";
        // reset dropzone background
        document.querySelectorAll('.dropzone').forEach(function(dropzone) {
            dropzone.classList.remove('dropzone-dragging');
        });
    }, false);

    document.addEventListener("dragover", function(event) {
        // prevent default to allow drop
        event.preventDefault();
    }, false);

    document.addEventListener("dragenter", function(event) {
        // highlight potential drop target when the draggable element enters it
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "#a3a3a3";
        }
    }, false);

    document.addEventListener("dragleave", function(event) {
        // reset background of potential drop target when the draggable element leaves it
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "";
        }
    }, false);

    document.addEventListener("drop", function(event) {
        event.preventDefault();

        // move dragged elem to the selected drop target
        if (event.target.classList.contains("dropzone")) {
            event.target.style.background = "";

            // Get the ID of the dragged accordion from the data transfer object
            const draggedAccId = event.dataTransfer.getData("draggedAccId");
            const draggedAcc = document.getElementById(draggedAccId);
            const fromContainer = draggedAcc.parentNode;
            const toContainer = event.target;

            // Check if the drop zone is already occupied, if so swap containers, if not append
            if (toContainer !== fromContainer) {
                const existingAcc = toContainer.firstElementChild;
                if (existingAcc) {
                    fromContainer.appendChild(existingAcc);
                }
                toContainer.appendChild(draggedAcc);
            } else {
                toContainer.appendChild(draggedAcc);
            }
        }
    }, false);
});

