function confirmDelete() {
    document.getElementById("delete-popup").style.display = "flex";
}

function closePopup() {
    document.getElementById("delete-popup").style.display = "none";
}

function submitDelete() {
    document.getElementById("delete-form").submit();
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function uploadPicture(event) {
    console.log("Upload triggered");
    const fileInput = event.target;
    const formData = new FormData();
    formData.append('profile_picture', fileInput.files[0]);

    fetch('upload_picture/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data);  // Log response to verify success
            // Optionally, update the profile picture display on success
            console.log(data.new_picture_url)
            document.getElementById("profile-picture").src = data.new_picture_url;
        } else {
            alert("Failed to upload the picture.");
        }
    })
    .catch(error => console.error("Error:", error));
}

