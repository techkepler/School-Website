import React from "react";
import { MessengerChat } from "react-messenger-chat-plugin";
import { useAuth } from "../../../contexts/GlobalProvider";

const Messenger = () => {
  const { currentLocation } = useAuth();
  return (
    <div
      className={`${
        currentLocation === "Home" ? "block lg:block" : "lg:hidden"
      }`}
    >
      <MessengerChat
        pageId="109100928577220"
        language="en_US"
        themeColor={"#40c3f7"}
        bottomSpacing={30}
        loggedInGreeting="Welcome to Asgard Academy !! If you have any question simply message us. Thank You !!"
        loggedOutGreeting="Thank you for connecting with  us. Thank You !!"
        greetingDialogDisplay={"show"}
        debugMode={true}
      />
    </div>
  );
};

export default Messenger;
