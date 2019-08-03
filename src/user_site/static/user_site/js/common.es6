function onPageLoad(endpoint, callback) {
  const metaEndpoint = $('meta[name="endpoint"]').attr('content');
  if (metaEndpoint === endpoint) {
    console.debug('Execute callback for ' + endpoint);
    callback();
  }
}
