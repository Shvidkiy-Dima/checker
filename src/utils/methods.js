function convert_for_bar(data, interval) {
    console.log(data)
    let step = null;
    if (interval === 1) {
      step = 1;
    }
    if (interval === 2) {
      step = 2;
    }

    if (step){
        for(var i = 0; i < data.length; i++) {
            data.splice(i+step,1);
        }
    }

    let new_data = data.map((e) => {
      return {
        created: e.created,
        res_code: e.response_code,
        error: e.error,
        value: 100 / data.length,
        color: e.error ? "#eb4d4b" : "green",
      };
    });

    return new_data;
  }

  export default convert_for_bar