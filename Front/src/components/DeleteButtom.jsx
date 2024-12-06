import { useForm } from 'react-hook-form';

export const DeleteButtom = ({ url }) => {
    const { _, handleSubmit } = useForm();

    const onSubmit = (data) => {
      fetch(url, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .then(() => window.location.replace('/'))
        .catch((error) => console.error('Error:', error));
    };

    return (
      <form onSubmit={handleSubmit(onSubmit)}>
        <button type="submit">Eliminar</button>
      </form>
    );
  };
