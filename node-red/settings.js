module.exports = {
  uiPort: process.env.PORT || 1880,
  uiHost: '127.0.0.1',
  flowFile: 'flows.json',
  functionGlobalContext: {},
  logging: {console:{level:'info',metrics:false,audit:false}}
};
