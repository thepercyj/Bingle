const data = {
  columns: [
    {
      label: 'Name',
      field: 'name'
    },
    'Position',
    'Office',
    'Age',
    'Start date',
    'Salary',
  ],
  rows: [
    ["Tiger Nixon", "System Architect", "Edinburgh", "61", "2011/04/25", "$320,800"],
    ["Garrett Winters", "Accountant", "Tokyo", "63", "2011/07/25", "$170,750"],
    ["Ashton Cox", "Junior Technical Author", "San Francisco", "66", "2009/01/12", "$86,000"],
    ["Cedric Kelly", "Senior Javascript Developer", "Edinburgh", "22", "2012/03/29", "$433,060"],
    ["Airi Satou", "Accountant", "Tokyo", "33", "2008/11/28", "$162,700"],
    ["Brielle Williamson", "Integration Specialist", "New York", "61", "2012/12/02", "$372,000"],
    ["Herrod Chandler", "Sales Assistant", "San Francisco", "59", "2012/08/06", "$137,500"],
    ["Rhona Davidson", "Integration Specialist", "Tokyo", "55", "2010/10/14", "$327,900"],
    ["Colleen Hurst", "Javascript Developer", "San Francisco", "39", "2009/09/15", "$205,500"],
    ["Sonya Frost", "Software Engineer", "Edinburgh", "23", "2008/12/13", "$103,600"],
    ["Jena Gaines", "Office Manager", "London", "30", "2008/12/19", "$90,560"],
    ["Quinn Flynn", "Support Lead", "Edinburgh", "22", "2013/03/03", "$342,000"],
    ["Charde Marshall", "Regional Director", "San Francisco", "36", "2008/10/16", "$470,600"],
    ["Haley Kennedy", "Senior Marketing Designer", "London", "43", "2012/12/18", "$313,500"]
  ],
};

const instance = new mdb.Datatable(document.getElementById('datatable'), data)
const advancedSearchInput = document.getElementById('advanced-search-input');

const search = (value) => {
  let [phrase, columns] = value.split(' in:').map((str) => str.trim());

  if (columns) {
    columns = columns.split(',').map((str) => str.toLowerCase().trim());
  }

  instance.search(phrase, columns);
}

document.getElementById('advanced-search-button').addEventListener('click', (e) => {
  search(advancedSearchInput.value)
});

advancedSearchInput.addEventListener('keydown', (e) => {
  if (e.keyCode === 13) {
    search(e.target.value);
  }
})