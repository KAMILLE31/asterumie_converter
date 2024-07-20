// pages/api/proxy.js

import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { input } = req.body;
      const response = await axios.post('https://7217d6c6-9a1c-4d85-95ed-12a571faeb4d-00-28sglkbljybma.picard.replit.dev/', { input });
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Internal Server Error' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
