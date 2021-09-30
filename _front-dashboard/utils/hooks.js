import React from "react";

function InputHook(defaultValue = "", callback = null, max_length = null) {
  let [value, setValue] = React.useState(defaultValue);

  function onChange(event) {
    let current_value = event.target.value;
    if (max_length) {
      current_value = current_value.slice(0, max_length);
    }
    setValue(current_value);
    if (callback) {
      callback(current_value);
    }
  }
  return {
    el: {
      onChange,
      value,
    },
    value,
    clear() {
      setValue("");
    },
  };
}

export { InputHook };
