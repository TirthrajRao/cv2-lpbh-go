// Use the Sheets API to load data, one record per row.
var responses = [];
var dataRangeNotation = 'Customers!A2:M6';
gapi.client.sheets.spreadsheets.values.get({
  spreadsheetId: '1addGXK1YLW3Ig7Zqp6-Jk5b1bwrQjiBfWEp1syLfdA4',
  range: dataRangeNotation
}).then((sheetsResponse) => {
  var values = sheetsResponse.result.values;
  console.log(values)
  // For each record, create a new merged presentation.
  // for (var i = 0; i < values.length; ++i) {
  //   var row = values[i];
  //   var customerName = row[2]; // name in column 3
  //   var caseDescription = row[5]; // case description in column 6
  //   var totalPortfolio = row[11]; // total portfolio in column 12

  //   // Duplicate the template presentation using the Drive API.
  //   var copyTitle = customerName + ' presentation';
  //   var request = {
  //     name: copyTitle
  //   };
  //   gapi.client.drive.files.copy({
  //     fileId: templatePresentationId,
  //     requests: request
  //   }).then((driveResponse) => {
  //     var presentationCopyId = driveResponse.result.id;

  //     // Create the text merge (replaceAllText) requests for this presentation.
  //     var requests = [{
  //       replaceAllText: {
  //         containsText: {
  //           text: '{{customer-name}}',
  //           matchCase: true
  //         },
  //         replaceText: customerName
  //       }
  //     }, {
  //       replaceAllText: {
  //         containsText: {
  //           text: '{{case-description}}',
  //           matchCase: true
  //         },
  //         replaceText: caseDescription
  //       }
  //     }, {
  //       replaceAllText: {
  //         containsText: {
  //           text: '{{total-portfolio}}',
  //           matchCase: true
  //         },
  //         replaceText: totalPortfolio
  //       }
  //     }];

  //     // Execute the requests for this presentation.
  //     gapi.client.slides.presentations.batchUpdate({
  //       presentationId: presentationCopyId,
  //       requests: requests
  //     }).then((batchUpdateResponse) => {
  //       var result = batchUpdateResponse.result;
  //       // Count the total number of replacements made.
  //       var numReplacements = 0;
  //       for (var i = 0; i < result.replies.length; ++i) {
  //         numReplacements += result.replies[i].replaceAllText.occurrencesChanged;
  //       }
  //       console.log(`Created presentation for ${customerName} with ID: ${presentationCopyId}`);
  //       console.log(`Replaced ${numReplacements} text instances`);
  //     });
  //   });
  // }
});