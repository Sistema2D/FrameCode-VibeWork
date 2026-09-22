---
schema: "fcvw/document@1"
artifact_role: "framework_policy"
owner: "framework"
upgrade_strategy: "replace"
---

# QA target execution guidance

Use only the rows relevant to the selected application. [QA](SKILL.md) owns the same discovery, execution, evidence and wiki-maintenance loop across disciplines; these are execution choices, not claims that adapters or equipment are installed. The host supplies available tools. Missing capabilities leave explicit blocked cases and an in-progress mapping checkpoint.

## Select by executable behavior

| Target | Initial mapping | How to act when capability is available | Evidence and limits |
|---|---|---|---|
| Web / browser UI | Routes, navigation, screens, buttons, forms, modals, responsive and accessible states | Available browser-control API; operate actual controls with semantic locators; inspect rendered outcomes | URL/build, browser/runtime, viewport, roles, observed states and redacted traces; HTTP checks alone do not prove UI behavior |
| Windows, Linux or macOS native desktop | Windows, dialogs, menus, controls, focus, files and process lifecycle | Available accessibility/native UI driver; keyboard/mouse when needed; launch the built application in its target OS | OS/architecture/build, driver, selected controls and observations; unsupported host/desktop session is blocked, not a simulated pass |
| Mobile / embedded GUI | Screens, navigation/back, permissions, orientation, lifecycle and device interactions | Available device/emulator UI control on the target platform | OS/device or emulator identity and lifecycle evidence; emulation does not establish physical sensor or device compatibility |
| CLI / batch / scripts | Commands, subcommands, flags, stdin, files, output, exit codes and signals | Run the actual executable in a disposable directory with bounded time; feed controlled inputs and check outputs/status/side effects | Exact command, tool/build, OS, stdout/stderr, exit code and resulting state; escape inputs and avoid secrets |
| APIs / services / distributed systems | Endpoints, schemas, auth roles, events, queues, workers, dependencies and failure paths | Use available protocol client/integration harness; start isolated services when authorized; correlate requests/events with observable results | Requests/responses, correlation IDs, status, logs and cleanup; mocked dependencies and untested integration boundaries remain explicit |
| C/C++, Rust or other native libraries | Public interfaces, arguments, errors, ownership/lifetimes, callbacks and concurrency contracts | Compile/run the project's harness using its supported toolchain; exercise the actual library; use sanitizers or analysis when relevant and available | Compiler/configuration, architecture, test binary, assertion/diagnostic output; compilation or static analysis alone is not a functional pass |
| Firmware / RTOS / bare metal | Boot/update/reset, tasks, states, memory/resource limits, interrupts, peripherals, serial/bus messages and outputs | Prefer existing emulator/SIL harness for its supported behavior; use authorized HIL/board access and instruments for physical behavior; bounded stimulus and observation | Firmware hash, board/revision or emulator, transport, tool settings, units and measured outputs; simulation never proves electrical, physical timing or hardware safety |
| Other / hybrid target | Exposed inputs, outputs, lifecycle, consumers and integration boundaries | Derive the interaction mode from project contracts; combine applicable rows or record a new project-specific mode with measurable observables | Identify which component and environment each result covers; unknown capability or intent stays blocked/unconfirmed |

## Multidisciplinary case selection

Cover function and domain invariants first. Add accessibility/usability for interactive surfaces; data integrity and permissions for stateful interfaces; portability and resource ownership for native code; concurrency, reliability and recovery for services; timing/resource/physical constraints for embedded systems. Performance tests require an approved workload, threshold, units and environment. Security checks remain within authorized scope and route to the security contract; do not turn functional QA into an unsolicited penetration test.

First execution maps every reachable relevant surface within the declared scope, including controls for GUIs and exposed interfaces/states for headless systems. Source inventories are discovery hints. If the target cannot execute, still record the source-backed inventory and blocked frontier; do not mark it fully mapped from source inspection alone. Record not-applicable dimensions with a reason, rather than creating fictional controls or passing tests.

## Physical and stateful actions

Honor the user's existing authorization. Before an operation outside that authorization, such as flashing firmware, driving actuators, changing bootloaders/fuses, destructive filesystem tests or altering production services, obtain the specific missing authority and safe target conditions. Capture/reset initial state and stop stimuli on fault. Do not infer electrical limits, timing tolerances, watchdog policy or safe actuator ranges; obtain them from the project's approved requirements. Lack of hardware or instrumentation blocks those checks, while independent simulator or host tests may proceed with clearly narrower coverage.

## Portable wiki representation

The [product contract](../../wiki/product/README.md) and templates work for all modes. Surface kinds include screen, modal, component, flow, cli, api, service, library, device, firmware and protocol. The machine field route is a stable logical entrypoint, not necessarily a URL: examples include cli:tool/status, cpp:Sensor::read, service:worker, uart:board/boot. Element locators can be accessible names, commands, API operations, symbols or protocol signals. Runtime records the actual OS/toolchain/driver/harness/device or simulator used; browser details are relevant only to browser runs. Retain exact commands and technical traces in evidence, with concise behavior descriptions in the wiki.
