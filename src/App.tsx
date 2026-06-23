import React, { useState } from 'react';

// Mock implementations for the problem domain
interface Phase {
    id: string;
    order: number;
}
interface Task {
    id: string;
    phaseId: string;
}

const syncPhaseToBackend = async (phase: Phase, method: string) => {
    return new Promise(resolve => setTimeout(resolve, 50));
};

const syncTaskToBackend = async (task: Task, method: string) => {
    return new Promise(resolve => setTimeout(resolve, 50));
};

const showToast = (message: string, actionText: string, action: () => void) => {
    console.log(message);
    action();
};

export const App = () => {
    const [phases, setPhases] = useState<Phase[]>([]);
    const [tasks, setTasks] = useState<Task[]>([]);

    const handleDeletePhaseUndo = async (phaseId: string) => {
        const phase = phases.find(p => p.id === phaseId);
        if (!phase) return;

        const relatedTasks = tasks.filter(t => t.phaseId === phaseId);

        try {
            await syncPhaseToBackend(phase, 'DELETE');
            setTasks(prev => prev.filter(t => t.phaseId !== phaseId));
            setPhases(prev => prev.filter(p => p.id !== phaseId));

            showToast('Fase excluída.', 'Desfazer', async () => {
                await syncPhaseToBackend(phase, 'POST');
                await Promise.all(relatedTasks.map(task => syncTaskToBackend(task, 'POST')));

                setPhases(prev => [...prev, phase].sort((a, b) => a.order - b.order));
            });
        } catch (error) {
            console.error(error);
        }
    }

    return <div>App</div>;
};
