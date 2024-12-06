import { useForm } from 'react-hook-form';
import { useState, useEffect } from 'react';
import links from '../../public/links.json';

export const FormToRole = ({ url, method }) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    data["name"] = data["name"].replace(/ /g, '_');
    fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error('Error:', error));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="text" {...register('name')} required/>
      <input type="text" {...register('description')} required/>
      <button type="submit">Enviar</button>
    </form>
  );
};

export const FormToUser = ({ url,method }) => {
  const { register, handleSubmit } = useForm();
  const [items, setItems] = useState([]);
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch(links['development-backend'].url + links['development-backend']['other-links'].sql.roles);
        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    };

    fetchItems();
  }, []); // Se ejecuta solo una vez

  const onSubmit = (data) => {
    let newurl = '';
    if (method === 'POST') {
      newurl = links['development-backend'].url + links['development-backend']['other-links'].sql.roles + "/" + data["role"] + links['development-backend']['other-links'].sql.user;
    } else {
      newurl = url;
    }
    fetch(newurl, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error('Error:', error));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="text" {...register('name')} required/>
      <input type="text" {...register('email')} required/>
      <input list="roles-list" {...register('role')} required/>
      <datalist id="roles-list">
        {items.length === 0 ?
          <option value="No hay roles creados todavia">No hay roles creados todavia</option> :
           items.map((item) => (
            <option key={item.id} value={item.name}>{item.name}</option>
          ))
        }
      </datalist>
      <button type="submit">Enviar</button>
    </form>
  );
};
