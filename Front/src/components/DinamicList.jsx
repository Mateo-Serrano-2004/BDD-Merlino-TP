import { useState, useEffect } from 'react';
import "./DinamicList.css";

const DynamicListContext = ({ refreshTrigger, url, redirection }) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      setLoading(true);
      try {
        const response = await fetch(url);
        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
      setLoading(false);
    };

    fetchItems();
  }, [refreshTrigger]); // Se ejecuta cada vez que `refreshTrigger` cambia

  if (loading) return <p>Cargando...</p>;

  if (items.length === 0) return <p>No hay elementos creados todavia</p>;

  return (
    <>
      {items.map((item) => (
        <a key={item.id} href={redirection + "/"+ (redirection === "/roles" ? item.name : item.id)}>{redirection.endsWith("/posts") ? item.text : item.name}</a>
      ))}
    </>

  );
};

const DinamicList = ({ url, redirection }) => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1); // Cambia el valor para forzar el re-renderizado
  };

  return (
    <div className='cover'>
      <button className='updateButton' onClick={handleRefresh}>Actualizar Lista</button>
      <DynamicListContext refreshTrigger={refreshTrigger} url={url} redirection={redirection} />
    </div>
  );
};

export default DinamicList;
