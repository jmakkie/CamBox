import { StyleSheet, View, StatusBar, Button, Alert } from "react-native";
import { WebView } from "react-native-webview";
import * as ScreenOrientation from "expo-screen-orientation"

// Main function
export default function Index() {
  async function changeScreenOrientation() {
    await ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.LANDSCAPE_LEFT);
  }
  
  changeScreenOrientation()

  // Returned views
  return (
    <View style={styles.container}>
      <StatusBar backgroundColor={"black"} barStyle={"default"} hidden/>
      
      {/* left button */}
      <View style={styles.ButtonContainer}>
        <Button
          title="Left"
          onPress={() => Alert.alert("pressed L")}
        />
      </View>
      
      {/* webview */}
        <WebView style={styles.WebView}
          source={{ uri: "http://192.168.113.92:5000" }}
        />
      
      {/* right button */}
      <View style={styles.ButtonContainer} >
        <Button
          title="Right"
          onPress={() => Alert.alert("pressed R")}
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
    backgroundColor: "#000000",
  },
  ButtonContainer: {
    justifyContent: "center",
    alignSelf: "stretch",
    backgroundColor: "#000000",
  },
});