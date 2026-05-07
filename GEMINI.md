# Diretrizes do Projeto

## Estilos e CSS
- **Centralização de CSS:** Todos os estilos personalizados, animações e componentes CSS devem ser definidos exclusivamente no arquivo `staticfiles/comum/src/input.css`.
- **Evitar Estilos Locais:** Não utilize blocos `<style>` dentro de templates HTML ou estilos inline (atributo `style`), para manter o código limpo e facilitar a manutenção global via Tailwind.
- **Classes Utilitárias:** Prefira criar classes utilitárias no `@layer components` do `input.css` para elementos recorrentes (formulários, botões, cards).
