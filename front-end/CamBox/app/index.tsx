import { StyleSheet, View, StatusBar, Button, Alert } from "react-native";
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
        <WebView style={styles.WebView}
          source = {{ uri: "http://192.168.113.92:5000" }} //change to use .env
        />

      <View style = {styles.ButtonContainer}>
        {/* flip camera button */}
        <Button
          title = "Flip"
          onPress = {() => switchCamera("flip")}
        />
        {/* next camera button */}
        <Button
          title = "Next"
          onPress = {() => switchCamera("next")}
        />
        {/* prev camera button */}
        <Button
          title = "prev"
          onPress = {() => switchCamera("prev")}
        />
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
  WebView: {
    flex: 1,
    backgroundColor: "#000000",
  },
  ButtonContainer: {
    justifyContent: "center",
    flexDirection: "row",
    alignSelf: "stretch",
    backgroundColor: "#000000",
  },
  Button: {
  },
});