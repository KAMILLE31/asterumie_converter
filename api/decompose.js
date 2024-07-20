// pages/api/decompose.js

export default async function handler(req, res) {
    if (req.method === 'POST') {
      try {
        const { input } = req.body;
        const decomposedStr = decomposeString(input);
        res.status(200).json({ output: decomposedStr });
      } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ message: 'Internal Server Error' });
      }
    } else {
      res.setHeader('Allow', ['POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  
  function decomposeHangul(syllable) {
      const BASE_CODE = 44032;
      const CHOSUNG = 588;
      const JUNGSUNG = 28;
  
      const CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
      const JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'];
      const JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
  
      const charCode = syllable.charCodeAt(0) - BASE_CODE;
      const chosungIndex = Math.floor(charCode / CHOSUNG);
      const jungsungIndex = Math.floor((charCode - (CHOSUNG * chosungIndex)) / JUNGSUNG);
      const jongsungIndex = charCode - (CHOSUNG * chosungIndex) - (JUNGSUNG * jungsungIndex);
  
      return {
          chosung: CHOSUNG_LIST[chosungIndex],
          jungsung: JUNGSUNG_LIST[jungsungIndex],
          jongsung: JONGSUNG_LIST[jongsungIndex]
      };
  }
  
  function decomposeString(inputStr) {
      let result = '';
      
      for (const char of inputStr) {
          if (char >= '가' && char <= '힣') {
              const { chosung, jung
  