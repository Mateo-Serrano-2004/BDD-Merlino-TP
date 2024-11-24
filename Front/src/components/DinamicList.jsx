import { useState, useEffect } from 'react';

const DynamicListContext = ({ refreshTrigger, url }) => {
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

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.nombre}</li>
      ))}
    </ul>
  );
};

const DinamicList = ({ url  }) => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1); // Cambia el valor para forzar el re-renderizado
  };

  return (
    <div>
      <button onClick={handleRefresh}>Actualizar Lista</button>
      <DynamicListContext refreshTrigger={refreshTrigger} url={url} />
    </div>
  );
};

export default DinamicList;
