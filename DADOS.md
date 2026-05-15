# Dados, Persistência e Migração

Documento metodológico para orientar como a aplicação armazena, lê, protege, migra, exporta, importa e descarta dados.

Este arquivo deve ser consultado antes de alterações em banco de dados, arquivos locais, JSON, cache, logs, vaults, histórico de conversas, configurações, importação, exportação, backup, migração ou retenção.

## Objetivo

Garantir que dados do usuário e dados versionados sejam tratados de forma segura, previsível, auditável e compatível com o versionamento da aplicação.

## Princípios

- Dados do usuário não devem ser versionados.
- Dados versionados devem ser separados de dados gerados em runtime.
- Toda escrita crítica deve considerar backup, escrita atômica ou rollback.
- Migrações devem ser idempotentes sempre que possível.
- Dados corrompidos devem ser tratados sem perda silenciosa.
- Dados sensíveis não devem ser registrados em logs.
- Mudanças de formato devem ser registradas em plano e changelog.

## Classificação dos dados

Todos os dados manipulados pela aplicação devem ser classificados em uma das quatro categorias abaixo. A classificação determina onde o dado pode ser armazenado, se pode ser versionado, como deve ser protegido e o que acontece quando é descartado.

As categorias são: **versionados** (fazem parte do repositório), **de usuário** (gerados pelo uso), **temporários** (recriáveis sem perda) e **sensíveis** (exigem proteção adicional). Um dado pode pertencer a mais de uma categoria.

## Dados atuais do projeto

Preencha esta seção ao instanciar o framework.

| Dado | Local | Classificação | Versionado |
|---|---|---|---|
| `<nome do dado>` | `<caminho/local>` | `<versionado/usuario/temporario/sensivel>` | `<sim/nao>` |

Quando o projeto possuir uma wiki de governança e também dados de usuário em formato Markdown, diferencie explicitamente as duas estruturas.

### Dados versionados

Fazem parte do repositório e podem ser distribuídos com a aplicação.

Exemplos:

- catálogos offline;
- templates;
- assets;
- documentação;
- configurações padrão sem segredos.

### Dados de usuário

Gerados ou modificados pelo uso da aplicação.

Exemplos:

- configurações pessoais;
- histórico de conversas;
- notas locais;
- arquivos importados;
- banco local;
- logs de uso.

### Dados temporários

Podem ser recriados sem perda funcional relevante.

Exemplos:

- cache;
- arquivos intermediários;
- builds;
- índices gerados;
- resultados transitórios.

### Dados sensíveis

Exigem proteção adicional.

Exemplos:

- tokens;
- chaves;
- credenciais;
- dados pessoais;
- dados de saúde;
- documentos privados;
- conteúdo confidencial de conversas.

## Regras de versionamento de dados

- Dados de usuário devem ficar fora do Git.
- Dados sensíveis nunca devem ser versionados.
- `.gitignore` deve cobrir logs, builds, caches, vaults locais e arquivos de configuração privada.
- Arquivos de exemplo devem usar placeholders.
- Mudança em dado versionado exige changelog.

## Persistência em arquivos

Quando a aplicação usar arquivos locais:

- preferir formatos legíveis quando apropriado, como Markdown, JSON, YAML ou TOML;
- validar conteúdo antes de sobrescrever arquivo existente;
- usar escrita atômica para dados importantes;
- criar backup antes de reescrita crítica;
- tratar ausência de arquivo com criação segura;
- tratar arquivo corrompido com fallback documentado;
- registrar mudanças de schema.

## Persistência em banco de dados

Quando a aplicação usar banco de dados:

- documentar engine, versão e local de armazenamento;
- criar estratégia de migração;
- registrar scripts de criação e atualização;
- definir backup e restauração;
- separar dados de aplicação e dados de usuário quando possível;
- testar migração com dados anteriores;
- registrar rollback quando possível.

Se o projeto não usar banco de dados, registre isso explicitamente. A adoção futura de banco deve ser tratada como mudança de escopo e arquitetura, com plano, decisão arquitetural, análise de dados, segurança, testes e changelog.

## Migração de dados

Toda migração deve conter:

- versão de origem;
- versão de destino;
- dados afetados;
- transformação aplicada;
- backup antes da migração;
- comportamento em caso de falha;
- possibilidade de rollback;
- validação pós-migração.

## Regras para importação

- Todo arquivo importado deve ser tratado como não confiável.
- Validar extensão, tamanho e conteúdo.
- Bloquear paths perigosos.
- Não executar conteúdo importado.
- Preservar fonte bruta quando necessário.
- Registrar origem e data quando relevante.
- Tratar duplicidades.

## Regras para exportação

- Informar ao usuário o que será exportado.
- Não incluir segredos por padrão.
- Permitir formato legível quando aplicável.
- Registrar versão do schema no arquivo exportado.
- Documentar limitações de compatibilidade.

## Retenção e descarte

Definir, quando aplicável:

- por quanto tempo logs são mantidos;
- quando cache pode ser limpo;
- como excluir dados do usuário;
- como confirmar ações destrutivas;
- se exclusão é reversível;
- se há backup antes de excluir.

## Schema e compatibilidade

Todo formato persistido deve ter, quando aplicável:

- nome do schema;
- versão do schema;
- campos obrigatórios;
- campos opcionais;
- valores padrão;
- regras de validação;
- compatibilidade com versões anteriores.

## Checklist para mudanças de dados

- [ ] O tipo de dado foi classificado.
- [ ] O dado deve ou não ser versionado.
- [ ] O local de armazenamento foi definido.
- [ ] Há risco de dado sensível.
- [ ] Há backup antes de alteração destrutiva.
- [ ] Há migração, se o formato mudar.
- [ ] Há validação de arquivo corrompido ou entrada inválida.
- [ ] Há teste de leitura de dados antigos.
- [ ] `.gitignore` cobre dados privados.
- [ ] Changelog registra mudança de dados.

## Regra para wiki de governança

Quando houver `wiki/` de governança, ela deve ser tratada como documentação versionada e deve apontar para fontes formais ao registrar aprendizados.

A wiki de governança não deve copiar dados privados, logs sensíveis ou conteúdo de conversas sem anonimização e justificativa explícita.

---

## Modelos e Templates

Para registrar novos schemas de dados, utilize o modelo em:
`governança/TEMPLATE_DADOS_SCHEMA.md`
