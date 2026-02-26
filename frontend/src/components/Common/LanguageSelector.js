import React, { useState } from 'react';
import api from '../../services/api';
import { setLanguage } from '../../utils/i18n';

const LanguageSelector = () => {
  const [lang, setLang] = useState('EN');

  const handleSelect = async () => {
    try {
      await api.get(`/lang-select?lang=${lang}`);
      setLanguage(lang);
      alert('Language selected');
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <div>
      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        <option value="EN">English</option>
        <option value="UA">Українська</option>
      </select>
      <button onClick={handleSelect}>Select</button>
    </div>
  );
};

export default LanguageSelector;