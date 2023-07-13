import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.scss';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [items, setItems] = useState([]);
  const [editMode, setEditMode] = useState(false);
  const [editItemId, setEditItemId] = useState(null);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await axios.get('http://localhost:5000/items');
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleAddItem = async () => {
    if (inputValue) {
      try {
        await axios.post('http://localhost:5000/items', { name: inputValue });
        setInputValue('');
        fetchItems();
      } catch (error) {
        console.error('Error adding item:', error);
      }
    }
  };

  const handleEditItem = (id) => {
    const newName = prompt('Enter the new name');
    if (newName) {
      try {
        axios.put(`http://localhost:5000/items/${id}`, { name: newName });
        fetchItems();
      } catch (error) {
        console.error('Error editing item:', error);
      }
    }
  };

  const handleDeleteItem = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/items/${id}`);
      fetchItems();
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  return (
    <div className='container'>
      <p className='titulo'>Fullstack operativa CRUD</p>
      <p className='titulo1'>En esta página se pueden probar las operaciones CRUD que se guardan en una base de datos relacional MySQL.</p>

      <div className='subcontainer'><input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter an item"
        />
        <button onClick={handleAddItem}>{editMode ? 'Save' : 'Add'}</button>

        <button onClick={fetchItems}>Read from Database</button>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.name}
            <button className='button-edit' onClick={() => handleEditItem(item.id)}>Edit</button>
            <button onClick={() => handleDeleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
