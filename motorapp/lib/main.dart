import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart'; // For launching the website URL

void main() {
  runApp(const MotorFailureApp());
}

class MotorFailureApp extends StatefulWidget {
  const MotorFailureApp({super.key});

  @override
  MotorFailureAppState createState() => MotorFailureAppState();
}

class MotorFailureAppState extends State<MotorFailureApp> {
  bool isDarkMode = false; // Track theme state

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Motor Failure Prediction',
      debugShowCheckedModeBanner: false,
      theme: isDarkMode
          ? ThemeData.dark().copyWith(
              primaryColor: Colors.deepPurple,
              colorScheme: const ColorScheme.dark(primary: Colors.deepPurple),
              textTheme: const TextTheme(
                bodyMedium: TextStyle(fontFamily: 'Poppins', color: Colors.white),
              ),
            )
          : ThemeData.light().copyWith(
              primaryColor: Colors.pinkAccent,
              colorScheme: const ColorScheme.light(primary: Colors.pinkAccent),
              textTheme: const TextTheme(
                bodyMedium: TextStyle(fontFamily: 'Poppins', color: Colors.black),
              ),
            ),
      home: PredictionForm(
        isDarkMode: isDarkMode,
        toggleTheme: () {
          setState(() {
            isDarkMode = !isDarkMode; // Toggle between light and dark theme
          });
        },
      ),
    );
  }
}

class PredictionForm extends StatefulWidget {
  final bool isDarkMode;
  final VoidCallback toggleTheme;

  const PredictionForm({super.key, required this.isDarkMode, required this.toggleTheme});

  @override
  PredictionFormState createState() => PredictionFormState();
}

class PredictionFormState extends State<PredictionForm> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController motorTypeController = TextEditingController();
  final TextEditingController temperatureController = TextEditingController();
  final TextEditingController vibrationController = TextEditingController();
  final TextEditingController speedController = TextEditingController();
  final TextEditingController torqueController = TextEditingController();
  final TextEditingController loadController = TextEditingController();
  final TextEditingController currentController = TextEditingController();
  final TextEditingController humidityController = TextEditingController();

  String failureType = '';
  String remainingLife = '';
  String recommendation = '';
  bool isLoading = false; // Track loading state

  // Function to launch a website in browser
  Future<void> _launchURL(url) async {
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  Future<void> _predictMotorFailure() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        isLoading = true; // Start loading
      });

      final motorData = {
        'features': [
          motorTypeController.text,
          double.parse(temperatureController.text),
          double.parse(vibrationController.text),
          double.parse(speedController.text),
          double.parse(torqueController.text),
          double.parse(loadController.text),
          double.parse(currentController.text),
          double.parse(humidityController.text)
        ]
      };

      try {
        final response = await http.post(
          Uri.parse('https://motor-failure-prediction.onrender.com/predict'),
          headers: {'Content-Type': 'application/json'},
          body: json.encode(motorData),
        );

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          setState(() {
            failureType = 'Failure Type: ${data['predicted_failure_type']}';
            remainingLife = 'Remaining Life: ${data['predicted_remaining_life']}';
            recommendation = 'Recommendation: ${data['recommendation']}';
          });
        } else {
          setState(() {
            failureType = 'Error: Unable to fetch prediction';
          });
        }
      } catch (e) {
        setState(() {
          failureType = 'Error: $e';
        });
      }

      setState(() {
        isLoading = false; // End loading
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Motor Failure Prediction'),
        actions: [
          Switch(
            value: widget.isDarkMode,
            onChanged: (value) {
              widget.toggleTheme();
            },
            activeColor: Colors.white,
          ),
          IconButton(
            icon: const Icon(Icons.web),
            onPressed: () {
              _launchURL('https://www.yourwebsite.com');
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          // Gradient background
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: widget.isDarkMode
                    ? [Colors.deepPurple.shade800, Colors.deepPurple.shade400]
                    : [Colors.pinkAccent.shade100, Colors.pinkAccent.shade400],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
          ),
          // Main content with padding and rounded cards
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: ListView(
                children: <Widget>[
                  // Image related to motors
                  Image.asset(
                    'assets/motor_icon.png',
                    height: 100,
                    fit: BoxFit.cover,
                  ),
                  const SizedBox(height: 20),
                  // Fields wrapped in colorful cards with shadow
                  _buildInputCard(
                    controller: motorTypeController,
                    label: 'Motor Type (L/M/H)',
                  ),
                  _buildInputCard(
                    controller: temperatureController,
                    label: 'Temperature (°C)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: vibrationController,
                    label: 'Vibration (Hz)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: speedController,
                    label: 'Speed (RPM)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: torqueController,
                    label: 'Torque (Nm)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: loadController,
                    label: 'Load (%)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: currentController,
                    label: 'Current (A)',
                    keyboardType: TextInputType.number,
                  ),
                  _buildInputCard(
                    controller: humidityController,
                    label: 'Humidity (%)',
                    keyboardType: TextInputType.number,
                  ),
                  const SizedBox(height: 20),
                  // Predict button
                  ElevatedButton(
                    onPressed: _predictMotorFailure,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 15),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      'Predict Failure',
                      style: TextStyle(fontSize: 18),
                    ),
                  ),
                  const SizedBox(height: 20),
                  // Display results
                  if (failureType.isNotEmpty) _buildPredictionResult(),
                  if (isLoading) const LinearProgressIndicator(), // Loading bar
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Function to build text input fields in a stylish card
  Widget _buildInputCard({
    required TextEditingController controller,
    required String label,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Card(
      elevation: 5,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: TextFormField(
          controller: controller,
          decoration: InputDecoration(
            labelText: label,
            labelStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            border: InputBorder.none,
          ),
          keyboardType: keyboardType,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter $label';
            }
            return null;
          },
        ),
      ),
    );
  }

  // Function to display prediction results
  Widget _buildPredictionResult() {
    return Card(
      elevation: 10,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildResultText('Failure Type', failureType),
            _buildResultText('Remaining Life', remainingLife),
            _buildResultText('Recommendation', recommendation),
          ],
        ),
      ),
    );
  }

  // Helper method to display individual result fields
  Widget _buildResultText(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            '$label:',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          ),
          Text(
            value,
            style: const TextStyle(fontSize: 16),
          ),
        ],
      ),
    );
  }
}
