import { StyleSheet, View, StatusBar, TouchableOpacity, Text} from "react-native";
import { WebView } from "react-native-webview";
import * as ScreenOrientation from "expo-screen-orientation"
import { switchCamera } from "@/components/httpRequests";
import { useEffect } from "react";

// Main function
export default function Index() {

  useEffect(() => {
    const changeScreenOrientation = async () => {

    await ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.LANDSCAPE);
  };
  
  changeScreenOrientation()
  }, []);
  

  // Returned views
  return (
    <View style = {styles.container}
      onLayout = {async () => {
        await ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.LANDSCAPE);
      }}
    >
      <StatusBar backgroundColor={"black"} barStyle={"default"} hidden/>
      
      {/* webview */}
        <WebView style={styles.webView}
          source = {{ uri: "http://192.168.113.92:5000" }} //change to use .env
        />

      <View style = {styles.buttonContainer}>
        {/* flip camera button */}
        <TouchableOpacity style={styles.buttonFlip} onPress = {() => switchCamera("flip")}>
          <Text style={styles.buttonText}>Flip</Text>
        </TouchableOpacity>
        {/* next camera button */}
        <TouchableOpacity style={styles.buttonNext} onPress = {() => switchCamera("next")}>
          <Text style={styles.buttonText}>Next</Text>
        </TouchableOpacity>
        {/* prev camera button */}
        <TouchableOpacity style={styles.buttonPrev} onPress = {() => switchCamera("prev")}>
          <Text style={styles.buttonText}>Prev</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: "#000000",
    paddingHorizontal: 22, //change to safe area of phone (camera spot)
  },
  webView: {
    backgroundColor: "#000000",
  },
  buttonContainer: {
    justifyContent: "center",
    flexDirection: "row",
    backgroundColor: "#000000",
  },
  buttonFlip: {
    padding: 8,
    borderRadius: 7,
    borderWidth: 1,
    borderLeftWidth: 2,
    borderColor: "#000000",
    justifyContent: "center",
    backgroundColor: "#16A085",
  },
  buttonNext: {
    padding: 4,
    borderRadius: 7,
    borderWidth: 1,
    borderColor: "#000000",
    justifyContent: "center",
    backgroundColor: "#16A085",
  },
  buttonPrev: {
    padding: 4,
    borderRadius: 7,
    borderWidth: 1,
    borderRightWidth: 0,
    borderColor: "#000000",
    justifyContent: "center",
    backgroundColor: "#16A085",
  },
  buttonText: {
    padding: 8,
    textAlign: "center",
    fontSize: 20,
    color: "#FFFFFF",
  }
});