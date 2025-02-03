import React from "react";
import { Text, StyleSheet, View } from "react-native";
import { WebView } from "react-native-webview";

export default function Index() {
  return (
    <View style = {styles.container}>
      <WebView style = {styles.webview}
        source={{ uri: "http://192.168.178.92:5000/videofeed"}}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
  },
  webview: {
    flex: 1,
  },
});