
## BMI Calculator 
The BMI (Body Mass Index) Calculator is a simple and intuitive web application designed to help users calculate their BMI based on their weight and height. BMI is a widely used metric that provides an estimate of body fat, which can be used to assess whether an individual is underweight, of normal weight, overweight, or obese. This app allows users to input their personal details, such as name, age, gender, weight, and height, and then calculates and displays their BMI along with the corresponding weight category. The app also provides an option to download a PDF receipt containing the BMI results, making it convenient for users to save or share their information.

## Technologies Used
- **Streamlit:** Streamlit is a Python framework used to build and share web applications quickly. In this app, Streamlit provides the structure and interactive components, such as input fields, buttons, and dynamic text display, to facilitate user interaction.

- **FPDF:** FPDF is a Python library for generating PDF files. In this app, FPDF is used to create a PDF receipt containing the user's BMI results. The receipt is generated on the fly and offered for download directly from the app.
- **CSS and JavaScript (via Streamlit Markdown):** Custom CSS is embedded within the app to enhance its visual appearance, making it responsive to both light and dark modes. A media query detects the user's system theme and adjusts the background, text, and input colors accordingly.

- **Base64 Encoding:** The app uses Base64 encoding to convert the PDF file into a downloadable link. This method ensures that the user can download the PDF without requiring server-side storage.

- **Pandas:**  Although not heavily used in this version of the app, Pandas is included to manage data and could be expanded for more complex data handling or additional features in future versions.



