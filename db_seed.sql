-- Usuários
INSERT INTO `usuarios` (`nome_completo`, `data_nascimento`, `cpf`, `email`, `senha`, `telefone`, `nivel`) VALUES
  ('Gabriela Rocha',    '1997-06-21', '789.012.345-66', 'ga123briela@example.com', '$2b$12$J3rXjxP1d4rG9IuF5/v7CuP3y8Edx4eLwbktIp5Wr.7ePpRJW1P7C', '47988881111', 'comum'),
  ('Diego Costa',       '2000-01-05', '456.789.012-33', 'diewdego@example.com', '$2b$12$C4qDgKj6xg8Kq8LrHnP9fOV1X0YfGcP.jfFy0uWjY4YI/o.Q6Pq6W', '47977772222', 'host-plus'),
  ('Ana Silva',         '1998-03-12', '123.456.789-01', 'weewq2@example.com', '$2b$12$uX.Ce4FbPoSxRpsp2A4x7.O1BlJpZxT7XzM1j3m6EGB4QZ3Zy8E6K', '47966663333', 'comum'),
  ('Henrique Alves',    '2003-12-03', '890.123.456-77', 'henrsdaique@example.com', '$2b$12$gHw7QbY9r5v6dFhXxQ9k4uqX5zHqv2k3KxCwzZxvM/IaGvFjv2d6O', '47955554444', 'host-premium'),
  ('Felipe Lima',       '2002-04-08', '678.901.234-55', 'fel1wdasipe@example.com', '$2b$12$Kx9dFh8qL1vG7uJcX5tQ0eX9y8RfYp3KqTzCwLxvM1bQ4ZyHj9rS', '47944445555', 'comum'),
  ('Bruno Pereira',     '2001-07-25', '234.567.890-11', 'brun2dao@example.com', '$2b$12$Vq8FpDk3tY1oM9wHhK3lQ2eX7y9LfYp4KsCwLxvN2bQ7ZxGjTj1Uq', '47933336666', 'host-standard'),
  ('Elisa Fernandes',   '1999-09-17', '567.890.123-44', 'elissa@example.com', '$2b$12$Rk4WpDq6vT2oN8xJjL5lQ3eY6y8LfYp5JsCwLxvO3bQ8YyHkVj2Ur', '47922227777', 'host-standard'),
  ('Carla Almeida',     '1995-11-30', '345.678.901-22', 'carl2312a@example.com', '$2b$12$Xj9MqDz7rP3pS7yKkL6nQ4fZ7y9PfYp6LsCwLxvP4bR9ZzHkUj3Uq', '47911118888', 'host-premium');

-- Endereços
INSERT INTO `enderecos` (`rua`, `numero`, `cidade`, `estado`, `complemento`, `usuario_id`) VALUES
  ('Rua das Flores', '123', 'Pomerode', 'SC', '', 1),
  ('Avenida Central', '456', 'Blumenau', 'SC', '', 2),
  ('Travessa do Sol', '78', 'Pomerode', 'SC', '', 3),
  ('Rua das Palmeiras', '22', 'Indaial', 'SC', '', 4),
  ('Avenida Brasil', '310', 'Blumenau', 'SC', '', 5),
  ('Rua João Pessoa', '55', 'Pomerode', 'SC', '', 6),
  ('Rua XV de Novembro', '99', 'Blumenau', 'SC', '', 7),
  ('Rua das Acácias', '12', 'Indaial', 'SC', '', 8);

-- Hospedagens
INSERT INTO `hospedagens` (`nome`, `descricao`, `endereco_id`, `usuario_id`) VALUES
  ('Pousada Florescer', 'Pousada aconchegante no centro de Pomerode', 1, 5),
  ('Hostel Central', 'Hostel moderno com café da manhã incluso', 2, 3),
  ('Apartamento Solar', 'Apartamento completo próximo ao centro', 4, 2),
  ('Casa do Lago', 'Casa ampla com quintal e piscina', 6, 1),
  ('Estadia XV', 'Flat confortável para temporada curta', 7, 6);
