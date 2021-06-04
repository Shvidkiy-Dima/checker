import React from "react";
import {Statistic} from 'antd'

export default function Timer({ monitor }) {
  const [seconds, setSeconds] = React.useState(0);

  React.useEffect(() => {
    setSeconds(monitor.last_request_in_seconds);
    const interval = setInterval(() => {
      setSeconds((seconds) => seconds + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [monitor.log.created]);

  return <div>{seconds + " sec ago"} </div>;
}
