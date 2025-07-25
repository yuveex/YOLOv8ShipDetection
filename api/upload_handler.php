<?php

header("Access-Control-Allow-Origin: *");

$upload_folder_path = "../images/uploads/"; // Uploads folder relative path

if(!isset($_FILES["image"])){
    echo json_encode(["result" => "ERROR", "message" => "No file uploaded!"]);
    exit;
}

$image_file = $_FILES["image"];
$unique_file_name = time() . "_" . basename($image_file["name"]);
$target_file_path = $upload_folder_path . $unique_file_name; // Filename: [time]_[imagename]

// Move to uploads folder
if(move_uploaded_file($image_file["tmp_name"], $target_file_path)){
    echo json_encode(["result" => "OK", "filePath" => $unique_file_name]);
}
else{
    echo json_encode(["result" => "OK", "message" => "File upload failed"]);
}

?>