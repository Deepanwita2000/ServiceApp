$(document).ready(function(){
    console.log("ajax is loaded!!")

    


        $(document).ready(function(){
            $("#add_service_btn").click(function(){
               
                // $("h1.text-centre").hide()
                $("#serviceForm").slideToggle();
                
            });
            });

        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        // Image preview on file select
        $("#icon").on("change", function (event) {
            const file = event.target.files[0];
            const preview = $("#imagePreview");  

            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.attr("src", e.target.result).show();
                };
                reader.readAsDataURL(file);
            } else {
                preview.attr("src", "").hide();
            }
        });


    //create or edit
    $("#service_register_btn").click(function(event){
        event.preventDefault()
        console.log("clicked")
        

        // input data
        const service_id= $("#service_id").val()
        const formData = new FormData($("#serviceForm")[0]);  //include all files,csrf etc

        console.log(formData)
        $.ajax({
            url : service_id? `/service/edit_service/${service_id}/` : `/service/add_service/`,
            method : "POST",
            data : formData,
            processData :false,
            contentType :false,
            success:function (response){
                $("#serviceForm")[0].reset();
                // $("#stream_register_btn").prop("disabled", true);

                // $("#stream_id").val("");
                // $("h3.text-primary").text("Stream Register");
                // $("#stream_register_btn").text("Save");
                 $("#serviceForm").hide()
                $("#imagePreview").hide(); // Hide image preview after submission
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut();

                $("#serviceList").html(response.services);

            },
            error:function(error){
                 const errorMessage = error.responseJSON?.message || "An error occurred.";
                $("#acknowledge").text(errorMessage)
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }



        })
    })


    // populate form for edit
    $(document).on("click" , ".edit-btn" , function (event){
        event.preventDefault()
        const service_id =$(this).data("id") 
        const name = $(this).data("name")
        const description = $(this).data("description")
        const icon = $(this).data("icon")
        console.log(service_id , name , description , icon)
        $("#service_id").val(service_id)
        $("#service_name").val(name)
        $("#description").val(description)
     
       
         // Show image preview if exists
        if (icon) {
            $("#imagePreview").attr("src", icon).show();
        } else {
            $("#imagePreview").hide();
        }

        $("h1.text-centre").text("Edit Service")
         $("#service_register_btn").text("Update");
    })

    
     // Delete Stream via AJAX
    $(document).on("click", ".delete-btn", function (event) {
        event.preventDefault();
        const service_id = $(this).data("id");
        const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        if (!confirm("AJAX: Are you sure you want to delete this stream?")) return;

        $.ajax({
            url: `/service/delete_service/${service_id}/`,
            method: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(2000).fadeOut();

                $("#serviceList").html(response.services); 
            },
            error: function () {
                $("#acknowledge").text("Failed to delete the stream.")
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }
        });
    })
})