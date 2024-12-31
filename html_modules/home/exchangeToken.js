const axios = require('axios');

exports.handler = async (event, context) => {
  const code = event.queryStringParameters.code;

  if (!code) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Authorization code missing' }),
    };
  }

  try {
    const response = await axios.post('https://api.fitbit.com/oauth2/token', null, {
      params: {
        client_id: 'YOUR_CLIENT_ID',
        client_secret: 'YOUR_CLIENT_SECRET',
        grant_type: 'authorization_code',
        redirect_uri: 'https://YOUR_NETLIFY_URL/.netlify/functions/exchangeToken',
        code,
      },
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token, refresh_token } = response.data;

    return {
      statusCode: 200,
      body: JSON.stringify({ access_token, refresh_token }),
    };
  } catch (error) {
    console.error(error.response.data);

    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Error exchanging authorization code' }),
    };
  }
};
