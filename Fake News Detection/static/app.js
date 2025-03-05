document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form")
    const fileInput = document.querySelector("#file")
    const fileUpload = document.querySelector(".custum-file-upload")
    const textSpan = fileUpload.querySelector(".text span")
    const textarea = document.querySelector("#news_text")
  
    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) {
        const fileName = e.target.files[0].name
        textSpan.textContent = `Selected: ${fileName}`
        textarea.disabled = true
        textarea.placeholder = "Image uploaded. Text will be extracted from the image."
        fileUpload.style.borderColor = "#007bff"
      } else {
        textSpan.textContent = "Click to upload image"
        textarea.disabled = false
        textarea.placeholder = "Enter news text here..."
        fileUpload.style.borderColor = "#e8e8e8"
      }
    })
  
    form.addEventListener("submit", (e) => {
      e.preventDefault()
      if (fileInput.files.length === 0 && textarea.value.trim() === "") {
        alert("Please enter some news text or upload an image.")
        return
      }
      form.submit()
    })
  })
  
  