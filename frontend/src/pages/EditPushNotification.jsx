import React from 'react';
import Action from './Action';
// hi

const EditPushNotification = ({ titles, bodies, onTitleChange, onBodyChange }) => {
    return (
        <div className="flex items-start w-full flex-grow">
            {/* Title Text Column */}
            <div className="flex flex-col p-1 h-full w-1/4 ml-7">
                <h3 className="font-bold mb-2">Title Text</h3>
                <div className="flex-grow flex flex-col justify-between">
                    {titles.map((title, index) => (
                        <input
                            key={index}
                            type="text"
                            value={title}
                            onChange={(e) => onTitleChange(index, e.target.value)}
                            className="block w-full h-full mb-2 p-2 border border-gray-300 rounded"
                        />
                    ))}
                </div>
            </div>

            {/* Body Text Column */}
            <div className="flex flex-col p-1 h-full w-3/5 ml-6">
                <h3 className="font-bold mb-2">Body Text</h3>
                <div className="flex-grow flex flex-col justify-between">
                    {bodies.map((body, index) => (
                        <input
                            key={index}
                            type="text"
                            value={body}
                            onChange={(e) => onBodyChange(index, e.target.value)}
                            className="block h-full mb-2 p-2 border border-gray-300 rounded"
                        />
                    ))}
                </div>
            </div>

            <div className="flex flex-col p-1 h-full ml-2">
                <h3 className="font-bold mb-2">Actions</h3>
                <Action />
                <Action />
                <Action />
                <Action />
                <Action />
            </div>
        </div>
    );
};

export default EditPushNotification;