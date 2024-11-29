import { useForm } from 'react-hook-form';

const FormToRole = ({ url, method }) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = (data) => {
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
      <input type="text" {...register('name')} />
      <input type="text" {...register('description')} />
      <button type="submit">Enviar</button>
    </form>
  );
};

export default FormToRole;
