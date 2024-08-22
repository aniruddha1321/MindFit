import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import Constants from 'expo-constants';
import * as Print from 'expo-print';
import * as Sharing from 'expo-sharing';
import { Picker } from '@react-native-picker/picker';

const BmiCalculator = () => {
    const [name, setName] = useState(''); // State to store the user's name
    const [gender, setGender] = useState(''); // State to store the user's gender
    const [weight, setWeight] = useState('');
    const [height, setHeight] = useState('');
    const [bmi, setBmi] = useState('');
    const [description, setDescription] = useState('');

    // Diet plans for each BMI category
    const dietPlans = {
        underweight: `
            <h2>Diet Plan for Underweight</h2>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <tr>
                    <th>Meal</th>
                    <th>Food Items</th>
                </tr>
                <tr>
                    <td>Breakfast</td>
                    <td>High-calorie smoothie, eggs, avocado</td>
                </tr>
                <tr>
                    <td>Lunch</td>
                    <td>Chicken sandwich, salad with nuts</td>
                </tr>
                <tr>
                    <td>Snack</td>
                    <td>Greek yogurt with honey, mixed nuts</td>
                </tr>
                <tr>
                    <td>Dinner</td>
                    <td>Grilled salmon, quinoa, steamed vegetables</td>
                </tr>
                <tr>
                    <td>Evening Snack</td>
                    <td>Peanut butter on whole grain toast</td>
                </tr>
            </table>
        `,
        normal: `
            <h2>Diet Plan for Normal</h2>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <tr>
                    <th>Meal</th>
                    <th>Food Items</th>
                </tr>
                <tr>
                    <td>Breakfast</td>
                    <td>Oatmeal with fruit, nuts, and yogurt</td>
                </tr>
                <tr>
                    <td>Lunch</td>
                    <td>Grilled chicken salad with mixed greens</td>
                </tr>
                <tr>
                    <td>Snack</td>
                    <td>Apple slices with almond butter</td>
                </tr>
                <tr>
                    <td>Dinner</td>
                    <td>Baked fish with vegetables and brown rice</td>
                </tr>
                <tr>
                    <td>Evening Snack</td>
                    <td>Handful of mixed nuts</td>
                </tr>
            </table>
        `,
        overweight: `
            <h2>Diet Plan for Overweight</h2>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <tr>
                    <th>Meal</th>
                    <th>Food Items</th>
                </tr>
                <tr>
                    <td>Breakfast</td>
                    <td>Greek yogurt with berries and chia seeds</td>
                </tr>
                <tr>
                    <td>Lunch</td>
                    <td>Quinoa salad with vegetables and chickpeas</td>
                </tr>
                <tr>
                    <td>Snack</td>
                    <td>Carrot sticks with hummus</td>
                </tr>
                <tr>
                    <td>Dinner</td>
                    <td>Grilled chicken breast with steamed broccoli</td>
                </tr>
                <tr>
                    <td>Evening Snack</td>
                    <td>Small apple or pear</td>
                </tr>
            </table>
        `,
        obese: `
            <h2>Diet Plan for Obese</h2>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <tr>
                    <th>Meal</th>
                    <th>Food Items</th>
                </tr>
                <tr>
                    <td>Breakfast</td>
                    <td>Smoothie with spinach, banana, and protein powder</td>
                </tr>
                <tr>
                    <td>Lunch</td>
                    <td>Mixed green salad with grilled turkey</td>
                </tr>
                <tr>
                    <td>Snack</td>
                    <td>Celery sticks with almond butter</td>
                </tr>
                <tr>
                    <td>Dinner</td>
                    <td>Baked salmon with asparagus and cauliflower rice</td>
                </tr>
                <tr>
                    <td>Evening Snack</td>
                    <td>Handful of almonds</td>
                </tr>
            </table>
        `
    };

    // Function to calculate BMI and assign a description
    const calculateBmi = () => {
        const bmi = weight / ((height / 100) * (height / 100));
        setBmi(bmi.toFixed(1));

        if (bmi < 18.5) {
            setDescription("You are Underweight, consume more healthy calories");
        } else if (bmi >= 18.5 && bmi <= 24.9) {
            setDescription("You are normal, keep it up and Stay motivated");
        } else if (bmi >= 25 && bmi <= 29.9) {
            setDescription("You are Overweight, consume fewer calories and burn more");
        } else if (bmi >= 30) {
            setDescription("Obese, Hit the Gym");
        }
    };

    // Function to generate the PDF with the BMI result and diet plan
    const generatePdf = async () => {
        let dietPlan = '';

        // Determine the appropriate diet plan based on the BMI description
        if (description.includes("Underweight")) {
            dietPlan = dietPlans.underweight;
        } else if (description.includes("normal")) {
            dietPlan = dietPlans.normal;
        } else if (description.includes("Overweight")) {
            dietPlan = dietPlans.overweight;
        } else if (description.includes("Obese")) {
            dietPlan = dietPlans.obese;
        }

        const htmlContent = `
            <html>
            <body>
                <h1>BMI Result</h1>
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Gender:</strong> ${gender}</p>
                <p><strong>Height:</strong> ${height} cm</p>
                <p><strong>Weight:</strong> ${weight} kg</p>
                <p><strong>BMI:</strong> ${bmi}</p>
                <p><strong>Description:</strong> ${description}</p>
                ${dietPlan}
            </body>
            </html>
        `;

        // Generate PDF from HTML content
        const { uri } = await Print.printToFileAsync({ html: htmlContent });

        // Share the generated PDF
        await Sharing.shareAsync(uri);
    };

    return (
        <View style={styles.container}>
            <View style={styles.title}>
                <Text style={styles.titleText}>BMI Calculator</Text>
            </View>

            <View style={styles.TextInput}>
                {/* Input for Name */}
                <TextInput
                    style={styles.input}
                    value={name}
                    onChangeText={(text) => setName(text)}
                    placeholder='Enter your name'
                />

                {/* Dropdown for Gender */}
                <Picker
                    selectedValue={gender}
                    onValueChange={(itemValue) => setGender(itemValue)}
                    style={styles.input}
                >
                    <Picker.Item label="Select Gender" value="" />
                    <Picker.Item label="Male" value="Male" />
                    <Picker.Item label="Female" value="Female" />
                </Picker>

                <TextInput
                    style={styles.input}
                    value={height}
                    onChangeText={(text) => setHeight(text)}
                    placeholder='Height in cm'
                    keyboardType='numeric'
                />
                <TextInput
                    style={styles.input}
                    value={weight}
                    onChangeText={(text) => setWeight(text)}
                    placeholder='Weight in kg'
                    keyboardType='numeric'
                />
            </View>

            <TouchableOpacity
                style={styles.button}
                onPress={calculateBmi}
            >
                <Text style={styles.buttonText}>Calculate</Text>
            </TouchableOpacity>

            <View style={styles.resultView}>
                <Text style={styles.result}>Name: {name}</Text>
                <Text style={styles.result}>Gender: {gender}</Text>
                <Text style={styles.result}>BMI : {bmi}</Text>
                <Text style={styles.result}>{description}</Text>
            </View>

            {/* Button to generate and download PDF */}
            <TouchableOpacity
                style={styles.button}
                onPress={generatePdf}
            >
                <Text style={styles.buttonText}>Share pdf</Text>
            </TouchableOpacity>
        </View>
    );
};

export default BmiCalculator;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: Constants.statusBarHeight,
        backgroundColor: '#e0ecde',
    },
    title: {
        backgroundColor: '#2c6975',
        height: 80
    },
})