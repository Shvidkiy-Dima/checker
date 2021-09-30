function convert_for_bar(data, interval) {
  // if (data.length > 720) {
  //   let step = null;
  //   if (interval === 1) {
  //     step = 1;
  //   }
  //   if (interval === 2) {
  //     step = 2;
  //   }

  //   if (step) {
  //     for (var i = 0; i < data.length; i++) {
  //       data.splice(i + step, 1);
  //     }
  //   }
  // }



  // {'start': i.created,
  //                              'successful': i.is_successful,
  //                              'count': 1,
  //                              'error': i.error,
  //                              'res_code': i.response_code}

  // let new_data = data.map((e) => {
  //   return {
  //     created: e.created,
  //     res_code: e.response_code,
  //     error: e.error,
  //     value: 100 / data.length,
  //     color: e.successful ? "green": "#eb4d4b",
  //   };
  // });


  let count = 0
  for (let k in data){
    count += data[k]['count']
  }

  let new_data = data.map((e) => {
    return {
      start: e.start,
      end: e.end,
      res_code: e.res_code,
      error: e.error,
      value: (100 / count) * e.count,
      color: e.successful ? "green": "#eb4d4b",
    };
  });
  
  console.log(data)
  console.log(new_data)

  return new_data;
}

export default convert_for_bar;
